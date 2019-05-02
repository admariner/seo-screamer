import sys
import subprocess
import re


class docx2pdf:
    def __init__(self, folder, source, timeout=None):
        self.folder = folder
        self.source = source
        self.timeout = timeout

    def convert_to(self):
        args = [self.libreoffice_exec(), '--headless', '--convert-to', 'pdf', '--outdir', self.folder, self.source]

        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=self.timeout)
        filename = re.search('-> (.*?) using filter', process.stdout.decode())

        if filename is None:
            raise LibreOfficeError(process.stdout.decode())
        else:
            return filename.group(1)


    def libreoffice_exec(self):
        # TODO: Provide support for more platforms
        if sys.platform == 'darwin':
            return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
        return 'libreoffice'


class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output


if __name__ == '__main__':
    d = docx2pdf(sys.argv[1], sys.argv[2])
    print('Converted to ' + d.convert_to())
