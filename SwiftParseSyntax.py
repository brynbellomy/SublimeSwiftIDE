
import sublime, sublime_plugin
import subprocess, json
from os import path
from .helpers import *

class SwiftParseSyntaxCommand(sublime_plugin.TextCommand):
    def is_enabled(self): return True

    def run(self, edit, **kwargs):
        exclude = kwargs['exclude'] if 'exclude' in kwargs else ''

        self.run_with(self.view, edit)


    def run_with(self, view, edit):
        settings = sublime.load_settings('SwiftIDE.sublime-settings')
        presets  = settings.get('presets', {})

        with open('/tmp/asdf.swift', 'w') as file:
            contents = allText(view)
            file.write(contents)

        output     = runProcess("/usr/local/bin/sourcekitten", args=['syntax', '--file', '/tmp/asdf.swift'])
        decodedObj = json.loads(str(output))

        regions = {}
        for item in decodedObj:
            region = sublime.Region(item['offset'], item['offset'] + item['length'])
            scope = item['type']
            if scope not in regions:
                regions[scope] = []

            regions[item['type']] += [region]

        view.erase_regions('SwiftIDE')
        for key in regions.keys():
            regionsForScope = regions[key]
            view.add_regions('SwiftIDE', regionsForScope, 'support.function', '', sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE | sublime.DRAW_EMPTY_AS_OVERWRITE)







