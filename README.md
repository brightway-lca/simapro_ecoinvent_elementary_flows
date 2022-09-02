# simapro_ecoinvent_elementary_flows

This repository is a openly-developed and openly-available mapping of the elementary flow lists of ecoinvent 3.8 and SimaPro 9.4.

## Data formats

This repository follows the data fomats used in [GLAD Elementary Flow Resources](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources) repository:

* [Input flow lists](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/blob/master/Formats/FlowList.md)
* [Output flow mapping](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/blob/master/Formats/FlowMapping.md)

## Contributing

Additions to the existing mapping are done using Github Actions, and can be done manually or programmatically. If you are interested in contributing, please first check the `Status` directory, whose readme file describes the number and types of flows already mapped.

Contributions should come as pull requests from named branches. So, you should:

* Fork this repo
* Create a new branch with a descriptive name
* Work work work, and then commit
* Create a Pull Request, and put `@cmutel` in the Pull Request description

### Manual contributions

You can manually create new CSVs but matching the input data in `Mapping/Input/Flowlists`. In general, manual mapping is discouraged; it is better to do this in a Jupyter notebook so that the output is in the correct format, and you don't have to suffer to get the right format and datatypes. However, if you insist, you are welcome to try! Please make sure to follow the [Output flow mapping](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/blob/master/Formats/FlowMapping.md) exactly - the column names and order both matter.

### Programmatic contributions

Start by duplicating `Notebooks/Template matching notebook.ipynb`, and adding your own logic or extra input data. The result of your script should be a new CSV file in `Contribute`. You can then submit a pull request.
