# ProviderFunction

The provider function invokes the provider framework:
https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources-readme.html#provider-framework.

This is useful for initiating custom actions that should fail a CloudFormation stack if they do not succeed, such
as migrating databases.

Usage example:

```ts
// Create a Lambda function which should conform the to provider framework:
// https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.Provider.html#example
const handler = new lambda.Function(this, "Handler", {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: "index.handler",
  code: lambda.Code.fromInline(`
      exports.handler = async (event, context) => {
        return {
          PhysicalResourceId: '1234',
          NoEcho: true,
          Data: {
            hello: 'world',
          },
        };
      };
    `),
});

const vpc = Vpc.fromLookup(this, "Vpc", {
  vpcName: "main-vpc",
  tags: {
    Stack: "networking",
  },
});

new ProviderFunction(this, "ProviderFunction", {
  vpc,
  function: handler,
});
```
