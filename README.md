# CDK Constructs Package for OrcaBus

This repository contains reusable AWS CDK constructs for the OrcaBus platform. These constructs simplify the creation
and management of AWS infrastructure components while following best practices and OrcaBus-specific configurations.

Packages readme docs:

[View Documentation](./packages/docs/README.md)

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
cd dev
```

Use the predefined pnpm script to run CDK commands:

```sh
pnpm cdk <command>

```

### Documentation

The package documentation is automatically generated in Markdown format using `typedoc` and `typedoc-plugin-markdown`.  
Run `pnpm packages:generate-docs` to update the generated documentation. It follows the JSDoc convention.  

View the package documentation here: [View Documentation](./packages/docs/README.md)

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
