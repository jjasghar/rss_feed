# Feed Reader

This script is run by a cron job every 30 minutes, and downloads new stories from RSS feeds.
It then generates an Markdown file that is rendered by the HTML page.

Arguments:
Path to the Database
Path to the subscription yaml file

Outputs to the console, so pipe to a file.

Active Development by _me_ now, but thank you to [fly](https://lobste.rs/s/fu9ebt/reclaiming_web_with_personal_reader#c_ntxce7)
for the basis of me building off of this.

```yaml
- url: <url to the rss>
  freq: <how often you should check for the latest article>
  icon: <font-awesomes icon>
  title: <overrides the title?>
```

## License & Authors

If you would like to see the detailed LICENSE click [here](./LICENSE).

- Author: JJ Asghar <jjasghar@gmail.com>

```text
Copyright:: 2023- JJ Asghar

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

