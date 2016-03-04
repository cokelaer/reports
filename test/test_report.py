from reports import report




class Test_report():

    def teardown(self):
        import shutil
        shutil.rmtree("report")

    def test(self):
        r = report.Report()
        r.create_report(onweb=False)
