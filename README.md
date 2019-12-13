# K-Means Clustering processing block
## Introduction

This is a simple instructional [unsupervised classification](https://en.wikipedia.org/wiki/Cluster_analysis)
algorithm that provides a very simple demo of what is possible to do using UP42.

The goal of this project is to guide you through setting UP42 in your
geospatial pipeline. It shows how easy it is to setup a clustering
algorithm implemented in [scikit-learn](https://scikit-learn.org/stable/index.html) to
perform a simple classification.

It functions as an example processing block. The block functionality and performed
processing steps are described in more detail in
the [UP42 documentation: K-Means Clustering block](https://docs.up42.com/up42-blocks/processing/kmeans-clustering.html).

**Block Input**: any [AOI clipped](https://docs.up42.com/specifications/capabilities.html?highlight=aoi%20clipped#builtin-capabilities)

**Block Output**: [GeoTIFF](https://en.wikipedia.org/wiki/GeoTIFF) file.

## Requirements

This example requires the **Mac or Ubuntu bash**, an example using **Windows** will be provided shortly.
In order to bring this example block or your own custom block to the UP42 platform the following tools are required:


 - [UP42](https://up42.com) account -  Sign up for free!
 - [Python 3.7](https://python.org/downloads)
 - A virtual environment manager e.g. [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
 - [git](https://git-scm.com/)
 - [docker engine](https://docs.docker.com/engine/)
 - [GNU make](https://www.gnu.org/software/make/)


## Instructions

The following step-by-step instructions will guide you through setting up, dockerizing and pushing the example custom
block to UP42.

### Clone the repository

```bash
git clone https://github.com/up42/k-means-clustering.git
```

Then navigate to the folder via `cd k-means-clustering`.

### Installing the required libraries

First create a new virtual environment called `up42-kmeans`, for example by using
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/):

```bash
mkvirtualenv --python=$(which python3.7) up42-kmeans
```

Activate the new environment:

```bash
workon up42-kmeans
```

Install the necessary Python libraries via:

```bash
make install
```

## Testing the block locally

Before uploading the block to the UP42 platform, we encourage you to run the following local tests and validations to
ensure that the block works as expected, conforms to the UP42 specifications and could be successfully applied in a
UP42 workflow.

### Run the unit tests

By successfully running the implemented Python unit tests you can ensure that the block processing functionality works
as expected. This project uses [pytest](https://docs.pytest.org/en/latest/) for testing, which was installed in
the previous step. Run the unit tests via:

```bash
make test
```

### Validate the manifest

Then test if the block manifest is valid. The
[UP42manifest.json](https://github.com/up42/k-means-clustering/blob/master/blocks/k-means-clustering/UP42Manifest.json)
file contains the block capabilities. They define what kind of data a block accepts and provides, which parameters
can be used with the block etc. See the
[UP42 block capabilities documentation](https://docs.up42.com/reference/capabilities.html?highlight=capabilities).
Validate the manifest via:

```bash
make validate
```

### Run the end-to-end test

In order to run the final end-to-end (`e2e`) test the block code needs to be dockerized (put in a container that later on
would be uploaded to UP42). The end-to-end test makes sure the block's output actually conforms to the platform's requirements.

First build the docker image locally.

```bash
make build
```

Run the `e2e` tests with:

```bash
make e2e
```


## Pushing the block to the UP42 platform

First login to the UP42 docker registry. `me@example.com` needs to be replaced by your **UP42 username**,
which is the email address you use on the UP42 website.

```bash
make login USER=me@example.com
```

In order to push the block to the UP42 platform, you need to build the block Docker container with your
**UP42 USER-ID**. To get your USER-ID, go to the [UP42 custom-blocks menu](https://console.up42.com/custom-blocks).
Click on "`PUSH a BLOCK to THE PLATFORM`" and copy your USERID from the command shown on the last line at
"`Push the image to the UP42 Docker registry`". The USERID will look similar to this:
`63uayd50-z2h1-3461-38zq-1739481rjwia`

Pass the USER-ID to the build command:
```bash
make build UID=<UID>

# As an example: make build UID=63uayd50-z2h1-3461-38zq-1739481rjwia
```

Now you can finally push the image to the UP42 docker registry, again passing in your USER-ID:

```bash
make push UID=<UID>

# As an example: make push UID=63uayd50-z2h1-3461-38zq-1739481rjwia
```

**Success!** The block will now appear in the [UP42 custom blocks menu](https://console.up42.com/custom-blocks/) menu
and can be selected under the *Custom blocks* tab when building a workflow.

<p align="center">
  <img width="500" src="https://i.ibb.co/YpmwxY2/custom-block-successfully-uploaded.png">
</p>

### Optional: Updating an existing custom block

If you want to update a custom block on UP42, you need to build the Docker container with an updated version:
The default docker tag is `k-means-clustering` and the version is set to `latest`.

```bash
make build UID=<UID> DOCKER_TAG=<docker tag> DOCKER_VERSION=<docker version>

# As an example: docker build UID=63uayd50-z2h1-3461-38zq-1739481rjwia DOCKER_TAG=k-means-clustering DOCKER_VERSION=1.0
```

Then push the block container with the updated tag and version:

```bash
make push UID=<UID> DOCKER_TAG=<docker tag> DOCKER_VERSION=<docker version>

# As an example: make push UID=63uayd50-z2h1-3461-38zq-1739481rjwia DOCKER_TAG=k-means-clustering DOCKER_VERSION=1.0
```

## Questions and recommendations

Open a **github issue** in this repository; we are happy to answer your questions!