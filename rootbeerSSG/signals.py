from blinker import signal, NamedSignal

before_content_load: NamedSignal = signal('before_content_load')
during_content_load: NamedSignal = signal('during_content_load')
after_content_load: NamedSignal = signal('after_content_load')

before_content_render: NamedSignal = signal('before_content_render')
during_content_render: NamedSignal = signal('during_content_render')
after_content_render: NamedSignal = signal('after_content_render')

before_render_index: NamedSignal = signal('before_render_index')
during_render_index: NamedSignal = signal('during_render_index')
after_render_index: NamedSignal = signal('after_render_index')

before_render_archive: NamedSignal = signal('before_render_archive')
during_render_archive: NamedSignal = signal('during_render_archive')
after_render_archive: NamedSignal = signal('after_render_archive')