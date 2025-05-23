# CDK Constructs Package for OrcaBus

This repository contains reusable AWS CDK constructs for the OrcaBus platform. These constructs simplify the creation
and management of AWS infrastructure components while following best practices and OrcaBus-specific configurations.

Packages docs:

[View Documentation](./packages/docs/README.md)

Alternatively, you can view the package documentation on [constructs.dev](https://constructs.dev/packages/@orcabus/platform-cdk-constructs).

## Repository Structure

This monorepo is organized as follows:

- **`packages/`** – Contains reusable CDK constructs, such as `api-gateway` and `deployment-stack-pipeline`. These packages are published to the npm registry.
- **`dev/`** – A development workspace for testing and experimenting with the constructs.
- **`.github/workflows/`** – Contains GitHub Actions workflows for automating releases to the npm registry.

The repository is structured as a pnpm workspace with two workspaces:

1. `packages/` – For CDK constructs that will be published to the npm registry.
2. `dev/` – For development and testing purposes.

## Getting Started

### Prerequisites

Ensure you have the correct Node.js version installed:

```sh
node --version
# Expected output: v22.9.0
```

Set up `corepack` (if not already enabled):

```sh
npm install --global corepack@latest
corepack enable pnpm
```

### Install Dependencies

To install all required dependencies across workspaces, run:

```sh
pnpm install
```

### Development

Navigate to the `dev` directory:

```sh
pnpm clean
pnpm i
cd dev
```

Use the predefined pnpm script to run CDK commands:

```sh
pnpm cdk <command>

```

### Documentation

This package’s documentation is automatically generated in Markdown format using [typedoc](https://typedoc.org/) and [typedoc-plugin-markdown](https://github.com/tgreyuk/typedoc-plugin-markdown).  
To regenerate the documentation, run:

```sh
pnpm packages:generate-docs
```

The documentation follows the JSDoc convention and can be viewed locally at:  
[📄 View Generated Documentation](./packages/docs/README.md)

Additionally, [constructs.dev](https://constructs.dev/) automatically indexes packages compiled with the JSII compiler (as this package is). Once published to the npm registry, the documentation is also available on their site:  
🔗 [@orcabus/platform-cdk-constructs on constructs.dev](https://constructs.dev/packages/@orcabus/platform-cdk-constructs)

### Publishing

A GitHub Action is configured to automatically publish to the npm registry when a release is created.

To publish manually, ensure the following environment variables are set:

- `NPM_ACCESS_LEVEL`
- `NPM_TOKEN`

Then, build, package, and publish the constructs:

```sh
pnpm build
pnpm package
pnpm publish
```

Alternative, you may push a new release to the `main` branch. This will trigger the GitHub Action to publish the package automatically.

i.e

```shell
git pull origin main
git checkout main

gh release create 0.0.10-alpha.0 --title '0.0.10-alpha.0 release!' --notes-file 'release-notes.md'
```
