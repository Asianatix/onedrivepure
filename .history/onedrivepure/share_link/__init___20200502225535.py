from .handle_share_link import handle_link


def do_link(args):
    show_json = args.show_json
    save_dir = args.save_dir
    for link in args.rest:
        handle_link(link, save_dirshow_json=show_json, =save_dir)
