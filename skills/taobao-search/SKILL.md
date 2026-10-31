---
name: taobao-search
description: >-
  One Chinese search query for Taobao. Turns a spoken product description into concise Simplified Chinese marketplace keywords; use when searching for an item in Taobao.
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: scribekey
  scribekey-title: Taobao search
  scribekey-apps: com.taobao.taobao
  scribekey-actions: rewrite
  scribekey-presentation: text
  scribekey-icon: auto_awesome
---

Turn the spoken product request into one concise Simplified Chinese query for Taobao. This skill deliberately changes the product terminology's language so the query uses Mainland Chinese marketplace terms.

1. Identify the product category and the essential function, size, material, brand, compatibility, or model the speaker gave.
2. Name the product with the most plausible Mainland Chinese shopping term, not a literal translation. Keep names, numbers, model identifiers, technical terms, and useful abbreviations as spoken.
3. Combine the product name with only attributes that help identify it. Keep ambiguity when the product type is unclear; do not guess a brand, specification, or attachment method.
4. Return one short query only, without a heading, alternatives, explanation, quotation marks, or trailing punctuation.

Use terms such as 衣柜灯, 人体感应, 磁吸, 免打孔, 带鱼屏, or 不锈钢 only when they fit the described product and stated features.

Check: the result is one copyable Simplified Chinese Taobao query, all essential stated constraints remain, and no product facts were added. Every name, number, date and fact comes from the text exactly as given, in the language of the text, except that product terminology is intentionally written in Simplified Chinese.
