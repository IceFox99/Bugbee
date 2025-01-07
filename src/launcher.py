import subprocess
import os
import shutil
import sys


class Launcher:
    def __init__(self, config):
        self.config = config
        self.env = os.environ
        self.cwd = os.getcwd()
        self.project_name = os.path.basename(self.config.sourceFolder)
        self.root_project_path = os.path.join(self.config.generate_folder, 'project')
        self.base_project_path = os.path.join(self.root_project_path, '_base')
        self.buggy_project_path = os.path.join(self.root_project_path, '_buggy')
        self.run_project_path = os.path.join(self.root_project_path, '_run')


    def launch(self):
        print("Launch projects")
        print("copy base project tp running environment")
        # does it have to be asynchronized?
        shutil.rmtree(self.run_project_path)
        # does it have to be asynchronized?
        shutil.copytree(self.base_project_path, self.run_project_path)

        print("change cwd to " + self.run_project_path)
        os.chdir(self.run_project_path)

        print("executing base project")
        base_project_dir = self.run_project_path
        for command in self.config.base_command:
            if command.split(" ")[0] == "cd":
                base_project_dir = os.path.join(base_project_dir, command.split(" ")[1])
                continue

            base_run = subprocess.run(command.split(), cwd=base_project_dir, env=self.env, capture_output=True, text=True)
            # process standard output and error output
            if base_run.stdout:
                sys.stdout.write(base_run.stdout)
            if base_run.stderr:
                sys.stderr.write(base_run.stderr)
            # if asynchronized, process

        print("executing buggy project")
        buggy_project_dir = self.run_project_path
        for command in self.config.buggy_command:
            if command.split(" ")[0] == "cd":
                buggy_project_dir = os.path.join(buggy_project_dir, command.split(" ")[1])
                continue

            buggy_run = subprocess.run(command.split(), cwd=buggy_project_dir, env=self.env, capture_output=True, text=True)
            # process standard output and error output
            if buggy_run.stdout:
                sys.stdout.write(buggy_run.stdout)
            if buggy_run.stderr:
                sys.stderr.write(buggy_run.stderr)

        os.chdir(self.cwd)
        # does it have to be asynchronized?
        shutil.rmtree(self.run_project_path)
        print("finish peoject")
