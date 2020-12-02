$graph:
- baseCommand: otbcli_BandMath
  hints:
    DockerRequirement:
      dockerPull: terradue/otb-7.2.0:latest
  class: CommandLineTool
  id: clt
  inputs:
    inp1:
      inputBinding:
        position: 1
        prefix: -il
      type: string[]
    inp2:
      inputBinding:
        position: 2
        prefix: -exp 
      type: string
    inp3:
      inputBinding:
        position: 2
        prefix: -out 
      type: string
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /opt/anaconda/envs/env_otb/conda-otb/bin/:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/envs/notebook/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/condabin:/opt/anaconda/bin:/usr/lib64/qt-3.3/bin:/usr/share/java/maven/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
        PREFIX: /opt/anaconda/envs/env_otb
    ResourceRequirement: {}
 # stderr: std.err
 # stdout: std.out
- class: Workflow
  doc: OTB band math
  id: main
  inputs:
    image_list:
      doc: images to process
      label: images to process
      type: string[]
    expression:
      doc: band math expression
      label: band math expression
      type: string
    result: 
      doc: result
      label: result
      type: string
  label: OTB band math
  outputs:
  - id: wf_outputs
    outputSource:
    - node_1/results
    type:
      Directory
  steps:
    node_1:
      in:
        inp1: image_list
        inp2: expression
        inp3: result
      out:
      - results
      run: '#clt'
cwlVersion: v1.0
