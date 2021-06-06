from rootbeer import signals


@signals.during_content_load.connect
def hello(sender) -> None:
    print('hello! this was loaded during the content was loaded!')