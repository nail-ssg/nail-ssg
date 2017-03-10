# nail-ssg
Nail. Simple site generator

## config.yml
``` yaml
# config.yml v0.2
core:
  dist: site
  src: src
  currentNamespace: default
  modules: !!omap
    - static:
        state: on
    - collections:
        state: on
    - alias:
        state: on
    - pages:
        state: on
    - mixin:
        state: on
main:
  scan:
    dataFolders:
    - data
    types:
    - type: ignore
      rules: 
      - fileMask = descrption.txt
    - type: page
      rules:
      - fileMask = *.html
      - fileMask = *.part
      - fileMask = *.tpl
      - fileMask = *.page.js
      - fileMask = *.page.css
      - fileMask = *.page.yml
      - fileMask = *.page.json
      - fileMask = *.page.txt
    - type: data
      rules:
      - fileMask = *.data.yml
    - type: static
      rules:
      - fileMask = *.*

modify:
  - alias:
  - collections:
  - mixin:
  - pages:
      folder: pages
      dontCopy:
      otherAsStatic: true

builders:
  renders:
  - plain:
  - mustache:
  order:
    - static
    - pages
  static:
    folder: static
  pages:
  - noRename:
    - fileMask = index.html
  - rename:
    - ~\.page~~ # replace '.page' to empty string
    - ~((.*)\.html)~\1/index.html~
```

## page settings
``` yaml
# v0.2
$global:
  alias:
    name: aliasName
    namespace: default
  collections:
    - collectionName1
    - collectionName2
    - collectionName3
  neighbors:
    - collection: collectionName4
      direction: ascending
      fieldname: dataName1
      useAs: dataName3
      distance: 1
  renders:
    - type: jade
    - type: mustache
  use:
    css:
      from: css
      sort: '+line'
      offset: 0
      count: 10
  load:
    - var1: file1
    - var2: file2
$local:
  collections:
    css:
      - href: style1.css
        line: 10.312
      - href: style2.css
        line: 20
    js:
      - href: script1.js
        line: 10.312
      - href: script2.js
        line: 10.313
    load:
      var3: file3
      var4: file4
    loadCollections:
      var5: folder
dataName1: dataValue1
dataName2: dataValue2
```