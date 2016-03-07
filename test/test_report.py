from reports import Report
from easydev import TempFile
import os


class Test_report():

    def teardown(self):
        import shutil
        try:
            shutil.rmtree("report")
        except:
            pass

    def test(self):
        r = Report()
        r.create_report(onweb=False)

        # test setter
        r.filename = "index.html"
        r.directory = "report"

        r._init_report()

    def test_local(self):

        # here we test if a local template works and if
        # a name different from index.html works
        temp_filename = "example.html"
        with open(temp_filename, "w") as fin:
            fin.write("{{ test }}")
        try:
            r = Report(".", template_filename=temp_filename)
            r.jinja['test'] = 'youpi'
            r.create_report(onweb=False)
            with open("report/index.html", "r") as fin:
                data = fin.read() 
                assert data == 'youpi'
        except Exception:
            raise Exception
        finally:
            # cleanup
            os.remove(temp_filename)
    
