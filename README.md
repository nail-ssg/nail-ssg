# nail-ssg
Nail. Simple site generator

## config.yml
``` yaml
# config.yml v0.2
core:
  modules:
    static: on      # v0.1
    collections: on # v0.1
    alias: on       # v0.1
    pages: on       # v0.1
    mixin: off      # v0.1
  dist: site
  src: src
  currentNamespace: default
renders:
- plain:
- mustache:

scan:
  dataFolders:
  - data
  types:
  - type: ignore
    rules: 
    - fileMask = descrption.txt
  - type: page
    rules:
    - endOfName = .html
    - endOfName = .part
    - endOfName = .tpl
    - endOfName = .page.js
    - endOfName = .page.css
    - endOfName = .page.yml
    - endOfName = .page.json
    - endOfName = .page.txt
  - type: data
    rules:
    - endOfName = .data.yml
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