# simapro_ecoinvent_elementary_flows

This repository is a openly-developed and openly-available mapping of the elementary flow lists of ecoinvent 3.8 and SimaPro 9.4.

## Table of Contents

- [Background](#background)
- [Contributing](#contributing)
- [Authors](#authors)
- [Maintainers](#maintainers)
- [License](#license)

## Background

Translating across nomenclature lists is an eternal problem in many problem domains, including life cycle assessment. There have been many ad hoc mapping files and file formats over the years, but recently a large working group produced the [GLAD Elementary Flow Resources](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources) repository; we will use its data formats for both input files and flow mappings:

* [Input flow lists](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/blob/master/Formats/FlowList.md)
* [Output flow mapping](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/blob/master/Formats/FlowMapping.md)

Our objective is to improve on the UNEP workflow by making the process of creating the mappings transparent and open to any one who wants to contribute. In addition to other benefits, this should also make future updates easier.

## Workflow

This repository uses Github Actions to merge contributions, and update the documentation (including this file). Specifically:

* A contributor forks this repository and adds their mapping contribution as a new CSV file in the `Contribute` directory. Ideally these constributions will be generated programmatically, either via a Jupyter Notebook (added to `Notebooks`) or a script (added to `Scripts`).
* They create a pull request, which triggers Github Actions which check the validity of their mapping file, and checks whether the new mappings contradict existing mappings. If there are errors, an error log is created and attached to the pull request.
* If the pull request is accepted, a separate set of Github Actions are run which merge the new mappings into `Mapping/Output/Mapped_files`, and updates the `README.md` file and status reports.

## Status

Current status is reported in

## Contributing

Your contributions are welcome! This effort, and indeed consistent, high-quality LCA results, are only possible when we work together.

You will need a Github account.

Additions to the existing mapping are done using Github Actions, and can be done manually or programmatically. If you are interested in contributing, please first check the `Status` directory, whose readme file describes the number and types of flows already mapped.

Contributions should come as pull requests from named branches. So, you should:

* Fork this repo
* Create a new branch with a descriptive name
* Work work work, and then commit
* Create a Pull Request, and put `@cmutel` in the Pull Request description

## Authors

{{ authors }}

## Maintainers

* [Chris Mutel](https://github.com/cmutel/)
* [Tomás Navarrete](https://github.com/tngtudor)

## License

* Code: [BSD-3-Clause](https://github.com/brightway-lca/bw_processing/blob/master/LICENSE)
* Data: [Open Data Commons Public Domain Dedication and License v1.0](http://opendatacommons.org/licenses/pddl/)
