from rootbeer import signals


@signals.during_render_index.connect
def hello(sender, *args, **kwargs) -> None:
    print('hello! this was loaded during the index was rendered!')
    print('You can get things needed for rendering from "sender! like this:')
    print('"sender.content" will give you:')
    print(sender.content)