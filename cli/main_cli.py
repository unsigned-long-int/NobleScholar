import argparse

def main():
    parser = argparse.ArgumentParser(prog='Noble Scholar', description='DOI manager and validator.')
    args = parser.parse_args()
    if args.validate:
        print("check")

if __name__ == '__main__':
    main()