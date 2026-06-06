
---
layout: two-cols
---

# 算法实现 - 复现论文算法

- class UserCFRec func getUserSimilarity(self) 节选

```python
  print("computing similarity between users...")
  # 得到每个item被哪些user评价过
  item_users = dict()
  for u, item_ratings in self.train.items():
      for i in item_ratings.keys():
          item_users.setdefault(i, set())
          if self.train[u][i] > 0:
              item_users[i].add(u)
```

::right::

```python
  # 构建倒排表
  print("creating reverse-sorted table...")
  count = dict()
  user_item_count = dict()
  for i, users in item_users.items():
      for u in users:
          user_item_count.setdefault(u, 0)
          user_item_count[u] += 1
          count.setdefault(u, {})
          for v in users:
              count[u].setdefault(v, 0)
              if u == v:
                  continue
              count[u][v] += 1
```
```python
  # 构建用户相似度矩阵
  print("creating users similarity matrix...")
  userSim = dict()
  for u, related_users in count.items():
      userSim.setdefault(u, {})
      for v, cuv in related_users.items():
          if u == v:
              continue
          userSim[u].setdefault(v, 0.0)
          userSim[u][v] = cuv / math.sqrt(user_item_count[u] * user_item_count[v])
  json.dump(userSim, open('UserCFUsersSim.json', 'w'))
```

<!--
这个函数是用来计算用户相似度的
 -->