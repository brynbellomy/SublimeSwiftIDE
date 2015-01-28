
import sublime, sublime_plugin
import subprocess, json
from os import path
from .helpers import *

class SwiftParseStructureCommand(sublime_plugin.TextCommand):
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

        output     = runProcess("/usr/local/bin/sourcekitten", args=['structure', '--file', '/tmp/asdf.swift'])
        decodedObj = json.loads(str(output))

        allKinds = self.processObject(decodedObj)
        # allKinds = set(allKinds)

        jsonOutput = json.dumps(allKinds)
        with open('/tmp/asdf.json', 'w') as file:
            file.write(jsonOutput)


    def processObject(self, obj, kinds = {}):
        # if 'key.kind' in obj:
        #     kinds += [obj['key.kind']]

        if 'key.substructure' in obj:
            for child in obj['key.substructure']:
                if 'key.name' in child and 'key.kind' in child:
                    name = child['key.name']
                    kind = child['key.kind']
                    print("name = " + str(name) + " // kind = " + str(kind))

                    if kind not in kinds:
                        kinds[kind] = []

                    kinds[kind] += [name]

                kinds = self.processObject(child, kinds)


        return kinds













