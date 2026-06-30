from pathlib import Path
import shutil


class TemplateEngine:

    def copy_template(self, template_path: str, output_folder: str):

        template = Path(template_path)

        output = Path(output_folder) / "template_test_output.xlsx"

        shutil.copy2(template, output)

        return output
        