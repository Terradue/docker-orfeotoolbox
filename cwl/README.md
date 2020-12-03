## Process EO data with CWL

This is a simple example demonstrating how useful this OTB docker image can be.

The example does a simple band math with two Sentinel-2 bands.

To run the example you need cwltool (see here how to install it https://github.com/common-workflow-language/cwltool) and docker then do:

```console
cwltool bandmath.cwl bandmath.yml
```

`bandmath.cwl` is a simple CWL workflow invoking a command line tool.
 
`bandmath.yml` provides the parameters values to run the CWL workflow:

```yaml
image_list:
- /vsicurl/https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/53/H/PA/2019/10/S2B_53HPA_20191012_0_L2A/B08.tif
- /vsicurl/https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/53/H/PA/2019/10/S2B_53HPA_20191012_0_L2A/B04.tif
expression: "(im1b1 - im2b1) / (im1b1 + im2b1)"
result: ndvi.tif
```

This shows how to process EO data without installing OTB nor downloading the EO data
