# check-experiment-script
bash scripts and python for checking experiments

Note - see [check-experiment-session](https://github.com/timdrysdale/check-experiment-session) for a way to do this using bookings rather than potentially interrupting a user. TODO - integrate the two repos.


## Example usage

```
export ACCESSTOKEN_SECRET=$(cat ~/secret/your-relay-secret.pat)
./make-session-files-for.sh 30 41 spin
./update-tokens.sh
./check_all.sh spin 30 41 ../files/step.json ../results
```

This should give you something like this

```
$ tree
<snip>
├── results
│   ├── spin30-data-1659029847.json
│   ├── spin30-video-1659029849.ts
│   ├── spin31-data-1659029851.json
│   ├── spin31-video-1659029854.ts
│   ├── spin32-data-1659029856.json
│   ├── spin33-data-1659029860.json
│   ├── spin33-video-1659029863.ts
│   ├── spin34-data-1659029865.json
│   ├── spin34-video-1659029867.ts
│   ├── spin35-data-1659029870.json
│   ├── spin35-video-1659029872.ts
│   ├── spin36-data-1659029874.json
│   ├── spin36-video-1659029876.ts
│   ├── spin37-data-1659029879.json
│   ├── spin37-video-1659029881.ts
│   ├── spin38-data-1659029883.json
│   ├── spin38-video-1659029885.ts
│   ├── spin39-data-1659029888.json
│   ├── spin39-video-1659029890.ts
│   ├── spin40-data-1659029892.json
│   ├── spin40-video-1659029894.ts
│   ├── spin41-data-1659029897.json
│   └── spin41-video-1659029899.ts
```

```
$ cd results
$ ls -lh
total 2.9M
-rw-rw-r-- 1 tim tim  21K Jul 28 18:37 spin30-data-1659029847.json
-rw-rw-r-- 1 tim tim 235K Jul 28 18:37 spin30-video-1659029849.ts
-rw-rw-r-- 1 tim tim  21K Jul 28 18:37 spin31-data-1659029851.json
-rw-rw-r-- 1 tim tim 224K Jul 28 18:37 spin31-video-1659029854.ts
-rw-rw-r-- 1 tim tim  130 Jul 28 18:37 spin32-data-1659029856.json
-rw-rw-r-- 1 tim tim  21K Jul 28 18:37 spin33-data-1659029860.json
-rw-rw-r-- 1 tim tim 226K Jul 28 18:37 spin33-video-1659029863.ts
-rw-rw-r-- 1 tim tim  21K Jul 28 18:37 spin34-data-1659029865.json
-rw-rw-r-- 1 tim tim 231K Jul 28 18:37 spin34-video-1659029867.ts
-rw-rw-r-- 1 tim tim  21K Jul 28 18:37 spin35-data-1659029870.json
-rw-rw-r-- 1 tim tim 251K Jul 28 18:37 spin35-video-1659029872.ts
-rw-rw-r-- 1 tim tim  21K Jul 28 18:37 spin36-data-1659029874.json
-rw-rw-r-- 1 tim tim 220K Jul 28 18:37 spin36-video-1659029876.ts
-rw-rw-r-- 1 tim tim  21K Jul 28 18:38 spin37-data-1659029879.json
-rw-rw-r-- 1 tim tim 247K Jul 28 18:38 spin37-video-1659029881.ts
-rw-rw-r-- 1 tim tim  22K Jul 28 18:38 spin38-data-1659029883.json
-rw-rw-r-- 1 tim tim 227K Jul 28 18:38 spin38-video-1659029885.ts
-rw-rw-r-- 1 tim tim  22K Jul 28 18:38 spin39-data-1659029888.json
-rw-rw-r-- 1 tim tim 250K Jul 28 18:38 spin39-video-1659029890.ts
-rw-rw-r-- 1 tim tim  21K Jul 28 18:38 spin40-data-1659029892.json
-rw-rw-r-- 1 tim tim 238K Jul 28 18:38 spin40-video-1659029894.ts
-rw-rw-r-- 1 tim tim  22K Jul 28 18:38 spin41-data-1659029897.json
-rw-rw-r-- 1 tim tim 250K Jul 28 18:38 spin41-video-1659029899.ts
```

Note in this example that there is a problem with spin32 - no video file, and nothing beyond the step file commands in the data file.  This would then prompt checking that experiment for an issue, i.e. this checking process has helped us identify an issue very quickly.

The videos can be watched using VLC. The data files can be inspected using a text editor, or by plotting with the python files in this repo

TODO - include info on plotting the results.

