import { Construct } from "constructs";
import { Bucket, IBucket } from "aws-cdk-lib/aws-s3";
import { RemovalPolicy } from "aws-cdk-lib";

/**
 * The CodeBuild cache bucket.
 */
export const CODEBUILD_CACHE_BUCKET = "orcabus-codebuild-cache-383856791668";

export interface ICacheBucket {
  /**
   * The S3 bucket used to cache CodeBuild builds.
   */
  readonly cacheBucket: IBucket;
}

/**
 * Creates a cache bucket for use with CodeBuild.
 */
export class CodeBuildCacheBucket
  extends Construct
  implements ICacheBucket
{
  /**
   * The S3 bucket used to cache CodeBuild builds.
   */
  public readonly cacheBucket: IBucket;

  constructor(scope: Construct, id: string) {
    super(scope, id);

    this.cacheBucket = new Bucket(this, "CacheBucket", {
      bucketName: CODEBUILD_CACHE_BUCKET,
      versioned: false,
      removalPolicy: RemovalPolicy.RETAIN,
      enforceSSL: true,
    });
  }

  /**
   * Imports an existing cache bucket using resource lookups.
   * @param scope The scope in which to look up the artifact bucket.
   * @returns ICacheBucket
   */
  public static fromLookup(scope: Construct): ICacheBucket {
    const cacheBucket = Bucket.fromBucketAttributes(
      scope,
      "CacheBucket",
      {
        bucketName: CODEBUILD_CACHE_BUCKET,
      },
    );

    return {
      cacheBucket,
    };
  }
}
