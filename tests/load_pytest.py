import sys
import pytest
try:
    from addon_helper import zip_addon, copy_addon, cleanup
except Exception as e:
    print(e)
    sys.exit(1)

class SetupPlugin(object):
    def __init__(self, addon):
        self.addon = addon

    def pytest_configure(self, config):
        (self.bpy_module, self.zfile) = zip_addon(self.addon)
        copy_addon(self.bpy_module, self.zfile)
        config.cache.set("bpy_module", self.bpy_module)

    def pytest_unconfigure(self):
        cleanup(self.addon, self.bpy_module)
        print("*** test run reporting finished")

addon = "fake_addon"
try:
    exit_val = pytest.main(["tests"], plugins=[SetupPlugin(addon)])
except:
    exit_val = 1
sys.exit(exit_val)
