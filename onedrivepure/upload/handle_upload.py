import os
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import JoinableQueue
from queue import Empty

from ..share_link import handle_link
from ..utils.bar_custom import count_bar, message_bar, sleep_bar
from ..utils.help_func import get_remote_base_path, norm_path
from .file_uploader import get_upload_url, upload_file, upload_remote


def get_path(local_paths, remote_base_path):
    file_list = []
    for path in local_paths:
        if os.path.isfile(path):
            name = os.path.basename(path)
            remote_path = norm_path(os.path.join(remote_base_path, name))
            file_list.append((path, remote_path))
        else:
            base_path, _ = os.path.split(path)
            bar = count_bar(message="个文件夹已完成")
            for root, _, files in os.walk(norm_path(path)):
                for name in files:
                    local_path = os.path.join(root, name)
                    remote_path = norm_path(
                        os.path.join(
                            remote_base_path, root[len(base_path) :].strip("/"), name
                        )
                    )
                    file_list.append((local_path, remote_path))
                bar.postfix = [root]
                bar.update(1)
            bar.close()
    return file_list


def put(client, args):
    local_paths = args.rest[:-1]
    remote_base_path = get_remote_base_path(args.rest[-1])
    q = JoinableQueue()
    sleep_q = JoinableQueue()
    if not args.sharelink:
        file_list = get_path(local_paths, remote_base_path)
        [q.put(i) for i in file_list]

        def do_task(task):
            sleep_q.join()
            local_path, remote_path = task

            status, upload_url, sleep_time = get_upload_url(client, remote_path)

            if status == "good":
                result = upload_file(
                    local_path=local_path,
                    upload_url=upload_url,
                    chunk_size=args.chunk,
                    step_size=args.step,
                )
                if result is not True:
                    q.put(task)

            elif status == "sleep":
                q.put(task)
                if sleep_q.empty():
                    sleep_q.put(sleep_time)

            elif status == "exist":
                message_bar(remote_path="od:/" + remote_path, message="文件已存在")
            else:
                q.put(task)
                message_bar(
                    remote_path="od:/" + remote_path, message="发生错误 (稍后重试): " + status
                )
            q.task_done()

    else:

        links = local_paths

        if len(links) > 1:
            print("暂不支持多个分享链接，请分次上传")
        link = links[0]

        data, share_link = handle_link(link, args.save_dir, show_json=False)

        q = JoinableQueue()
        sleep_q = JoinableQueue()

        [q.put(t) for t in data]

        def do_task(task):

            sleep_q.join()

            download_url = task.get("download_url")
            file_size = task.get("size")
            remote_path = norm_path(os.path.join(remote_base_path, task.get("path")))

            status, upload_url, sleep_time = get_upload_url(client, remote_path)

            if status == "good":
                result = upload_remote(
                    download_url=download_url,
                    upload_url=upload_url,
                    share_link=share_link,
                    file_size=file_size,
                    remote_path=remote_path,
                    chunk_size=args.chunk,
                    step_size=args.step,
                )
                if result is not True:
                    q.put(task)

            elif status == "sleep":
                q.put(task)
                if sleep_q.empty():
                    sleep_q.put(sleep_time)

            elif status == "exist":
                message_bar(remote_path="OD:" + remote_path, message="文件已存在")
            else:
                q.put(task)
                message_bar(remote_path="OD:" + remote_path, message=status + " 稍后重试")
            q.task_done()

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        while True:
            if q._unfinished_tasks._semlock._is_zero():
                break
            elif not sleep_q.empty():
                sleep_time = sleep_q.get()
                sleep_bar(sleep_time=sleep_time)
                sleep_q.task_done()
            else:
                try:
                    task = q.get(timeout=args.sleep_time)
                except Empty:
                    continue
                else:
                    executor.submit(do_task, task)
                    time.sleep(args.sleep_time)

    return client
