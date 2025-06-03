# NamedLambdaRole

A construct for naming a role that is assumed by a Lambda function.

Usage example:

```ts
// This uses `lambda.amazonaws.com' as the `assumedBy` service principal.
new NamedLambdaRole(this, id, {
  name: "role-name",
  maxSessionDuration: Duration.hours(12),
});
```
