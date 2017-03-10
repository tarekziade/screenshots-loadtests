# SCENARIOS

1. `login()` (setup) :check:
1. `create_shot()` (file-bottleneck) :check:
  1. img_size_01
  1. img_size_02
  1. img_size_03
1. `read_shot()` (file-bottleneck)
1. `read_my_shots()`
1. `search_shots()` (db-bottleneck)
1. `delete_account()` (teardown) (db-bottleneck) :check:

---

## SCENARIOS

- create_user(session)
- create_image(session)
- display_image(session)
- list_images(session)
- delete_account(session)

## UTILS:

- login
- create_user()
- create_images(x,y,z)
- list_images(x,y,z)
- delete_account(user_id)
- etc.

