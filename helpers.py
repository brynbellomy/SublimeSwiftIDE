import sublime
import subprocess


# class Bryn:
#     @staticmethod
def allText(view):
    return view.substr(sublime.Region(0, view.size()))

#@staticmethod
def selText(view):
    text = []
    for region in view.sel():
        if region.empty():
            continue
        text.append(view.substr(region))
    return "".join(text)

#@staticmethod
def getText(view):
    text = Bryn.selText(view)
    if len(text) > 0:
        return text
    return Bryn.allText(view)


def runProcess(cmd, args = [], stdin="", cwd = None, env = None):
    if not type(args) is list:
        args = [args]

    cmdString  = " ".join([cmd] + args)
    byteOutput = subprocess.check_output(cmdString, cwd='/tmp', shell=True)
    # byteOutput = subprocess.check_output("/usr/local/bin/sourcekitten syntax --file /tmp/asdf.swift", cwd='/tmp', shell=True) # stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env,
    output = byteOutput.decode('utf8')
    return output


# @classmethod
def SortValueForRegion(region):
    return region.begin()

# @classmethod
def RegionToFullLine(view):
    def fn(region):
        begin = view.line(region).begin()
        end = region.end()
        region.a = begin
        region.b = end
        return region
    return fn

def regionToTuple(region):
    return (region.begin(), region.end())

def tupleToRegion(tpl):
    return sublime.Region(tpl[0], tpl[1])

def regionToTextInView(view):
    def fn(region): return view.substr(region)
    return fn

def filterDuplicateRegions(_list_regions):
    list_regions = list(set(map(Bryn.RegionToTuple, _list_regions)))
    list_regions =     list(map(Bryn.TupleToRegion, list_regions))
    return list_regions

def zoomToRegionInView(region, view):
    view.show_at_center(region)
    view.sel().clear()
    view.sel().add(region)

def mapWaterfall(obj, func_list):
    def recursiv(_obj, fl):
        if len(fl) > 0:
            func = fl[0]
            fl_tail = list(fl)
            fl_tail.remove(func)
            return recursiv(func(_obj), fl_tail)
        else:
            return _obj
    return recursiv(obj, func_list)

