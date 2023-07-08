import yaml


def get_options(file):
    with open(file, 'r') as f:
        options = yaml.safe_load(f)

    return options


if __name__ == '__main__':
    opts = get_options('./options.yaml')
    print(opts)
