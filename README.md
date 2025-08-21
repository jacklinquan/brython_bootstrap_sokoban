# brython_bootstrap_sokoban

This Sokoban Puzzle Game project is built with [Brython](https://brython.info/),
[Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/),
and [sokobanpy](https://github.com/jacklinquan/sokobanpy) Python package.

[Play Online](https://jacklinquan.github.io/brython_bootstrap_sokoban)

![sokoban qrcode](/img/sokoban_qr.png)

## Duplicating this project

1. Create a new GitHub repository and push all files from this project to it.
2. In your repository, go to **Settings → Actions → General**. Under **Workflow permissions**, select **Read and write permissions**, then **Save**.
3. Go to **Settings → Pages**. Under **Build and deployment → Branch**, choose **gh-pages** and **/(root)**, then **Save**.

## Adding or removing Sokoban level collections

1. In the project directory `website/assets/collections`, add or remove Sokoban level collection files (`*.slc`).
2. Regenerate the list by running:

```shell
python build_collection_list.py
```

This updates `collection_list.txt`.

The level collection `0Beginner` is designed by myself.
And all of the other level collections are downloaded from here:
[https://sourcecode.se/sokoban](https://sourcecode.se/sokoban)
