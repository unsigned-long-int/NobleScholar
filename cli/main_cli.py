import argparse
from abc import ABC, abstractmethod

class ActionTypeError(Exception):
    pass

class ArgsFactory:
    """ Handles assignment of correct polymorphic class instance depending on the type of actions
        Attributes: args() : argument NameSpace from argsparser
    """
    def __init__(self, args):
        self.args = args 
        args_manager_ptr = self._fetch_action_manager()
        self.args_instance = args_manager_ptr(**vars(self.args))

    def _fetch_action_manager(self):
        if self.args.command_type == 'file-manager':
            return FileArgsHandler
        if self.args.command_type = 'doi-manager':
            return DoiArgsHandler
        raise ActionTypeError(f'Missing action: {self.args.command_type}.')
    
    def process_args(self):
        self.args_instance.process_args()

class ArgsInterface(ABC):
    def __init__(self):
        self.process_args()

    @abstractmethod
    def fetch_action(self):
        raise NotImplementedError

    @abstractmethod
    def process_args(self):
        raise NotImplementedError


class FileArgsHandler(ArgsInterface):
    def __init__(self, file_path, extract_doi, validate_file, **kwargs):
        self.file_path = file_path
        self.extract_doi = extract_doi
        self.validate_file = validate_file
        #super().__init__()

    def fetch_action(self):
        if self.extract_doi:
            return extract_doi

        if self.validate_file:
            return validate_file

    def process_args(self):
        action_ptr = self.fetch_action()
        action_ptr(self.file_name)

class DoiArgsHandler(ArgsInterface):
    def __init__(self, doi_list, validate_doi, **kwargs):
        self.doi_list = doi_list 
        self.validate_doi = validate_doi
        self.dois = self._extract_dois()
        #super().__init__()

    def _extract_dois(self):
        return self.doi_list.split(',')

    def fetch_action(self):
        if self.validate_doi:
            return validate_doi

    def process_args(self):
        action_ptr = self.fetch_action()
        action_ptr(self.dois)


def main():
    global_parser = argparse.ArgumentParser(prog='Noble Scholar', description='DOI manager and validator.')
    subparsers = global_parser.add_subparsers(title='Actions', dest='command_type', description='set of possible actions', help='choose set of wanted actions')
    file_subparser = subparsers.add_parser(name='file-manager', description='these commands allow to work with file directly')
    file_subparser.add_argument('file_path', type=str, help='path to the file which will be extracted')
    file_options_group = file_subparser.add_mutually_exclusive_group()
    file_options_group.add_argument('-e', '--extract-doi', dest='extract_doi', action='store_true', help='extract all found DOIs from file')
    file_options_group.add_argument('-vf', '--validate-file', dest='validate_file', action='store_true', help='extract and validate all found DOIs')
    doi_subparser = subparsers.add_parser(name="doi-manager", description='these commands allow to work with DOIs directly')
    doi_subparser.add_argument('doi_list', type=str, help='list of comma-separated DOIs')
    doi_subparser.add_argument('-vd', '--validate-doi', dest='validate_doi', action='store_true', help='validates all DOIs against retraction db')
    args = global_parser.parse_args(['doi-manager', 'test', '-vd'])
    args_manager_instance = ArgsFactory(args=args)
    print(args_manager_instance)


if __name__ == '__main__':
    main()