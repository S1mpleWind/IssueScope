# O3：CI 门禁与可追踪发布证据

更新日期：2026-10-21  
项目：[IssueScope](https://github.com/S1mpleWind/IssueScope)

## 目标与实施

用自动化检查保护 `main`，让变更经 PR、审批和 CI 后合入；每个发布包包含前端构建产物及 `BUILD_INFO.json`，并提供 SHA-256 校验和。后端 `GET /api/version` 返回版本、Actions 构建号和源码 commit；`scripts/trace.sh` 可从归档中读取这些信息。

GitHub ruleset `main-branch`（ID `25532883`）处于 active，目标是默认分支，要求 PR、至少 1 个 approval 和 `ci` 检查，并禁止删除分支及 non-fast-forward 更新。规则可见 [GitHub ruleset](https://github.com/S1mpleWind/IssueScope/settings/rules/25532883)。PR #51、#52、#53、#54 均经过审批并合入 `main`。

发布 workflow `.github/workflows/release.yml` 仅响应 `vX.Y.Z` tag；发布前验证 tag commit 属于 `main` 历史，再跑后端与前端检查并生成归档、元数据和校验和。

## CI 门禁演练

- PR [#51](https://github.com/S1mpleWind/IssueScope/pull/51)：故意错误的前端期望值使 [run 39570727566](https://github.com/S1mpleWind/IssueScope/actions/runs/39570727566) 失败；修正后 [run 39570870332](https://github.com/S1mpleWind/IssueScope/actions/runs/39570870332) 通过。后端测试先通过，失败发生在前端测试。
- PR [#53](https://github.com/S1mpleWind/IssueScope/pull/53)：故意错误的后端断言使 [run 39572929615](https://github.com/S1mpleWind/IssueScope/actions/runs/39572929615) 在后端测试阶段失败；修正后 [run 39573041544](https://github.com/S1mpleWind/IssueScope/actions/runs/39573041544) 全部通过。
- 直接推送验证：空提交尝试更新 `main` 被 GitHub 以 `GH013` 拒绝，提示变更必须通过 PR；提交未进入 `main`。

本地验证：后端 177 passed、5 skipped；前端 lint、7 个测试和生产构建通过。Release 包解压后通过 FastAPI TestClient 请求 `/api/version`，得到 HTTP 200 和匹配该包的版本信息。

## Release 证据

### `v0.1.0`

- [GitHub Release](https://github.com/S1mpleWind/IssueScope/releases/tag/v0.1.0)，[tag](https://github.com/S1mpleWind/IssueScope/tree/v0.1.0)。
- Release Actions [run 39573212997](https://github.com/S1mpleWind/IssueScope/actions/runs/39573212997) 成功。
- 元数据：版本 `v0.1.0`，构建号 `1`，commit `79064d64571f0b9e486eeff7f554b481b6faa17c`。
- 归档 SHA-256：`bb4325ed218d64c59709f0eb2580b305518a3faf6c2f0a04e3daab2bb13af475`。
- 下载后 `sha256sum -c` 通过；`scripts/trace.sh` 和 `/api/version` 均读出相同元数据。

### `v0.1.1`

- [GitHub Release](https://github.com/S1mpleWind/IssueScope/releases/tag/v0.1.1)，[tag](https://github.com/S1mpleWind/IssueScope/tree/v0.1.1)。
- Release Actions [run 39584554209](https://github.com/S1mpleWind/IssueScope/actions/runs/39584554209) 成功。
- 元数据：版本 `v0.1.1`，构建号 `2`，commit `6adbe7d61d3185137506382afdf62ce30fa1985b`。
- 归档 SHA-256：`611acd2465374f0e6aef598af961fe154e924485f1abd98ba4c0c0e081aba4f5`。
- 下载后 `sha256sum -c` 通过；`scripts/trace.sh` 和 `/api/version` 均读出相同元数据。

### 实验中修复的问题

初版 `v0.1.0` checksum 记录了 CI 内部的 `dist/` 路径，下载后无法直接校验。修复 PR [#54](https://github.com/S1mpleWind/IssueScope/pull/54) 改为只记录归档文件名，其 CI [run 39573473967](https://github.com/S1mpleWind/IssueScope/actions/runs/39573473967) 通过并已合入。`v0.1.0` 的 checksum 资产也已重新上传并验证；`v0.1.1` 使用修正后的工作流生成，下载校验直接通过。

## GitHub 记录

演练和变更证据已通过 `gh pr comment` 记入：[#51 评论](https://github.com/S1mpleWind/IssueScope/pull/51#issuecomment-6311846624)、[#52 评论](https://github.com/S1mpleWind/IssueScope/pull/52#issuecomment-6311847332)、[#53 评论](https://github.com/S1mpleWind/IssueScope/pull/53#issuecomment-6313620265)、[#54 评论](https://github.com/S1mpleWind/IssueScope/pull/54#issuecomment-6313620702)。
