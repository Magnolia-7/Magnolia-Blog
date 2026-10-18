<template>
  <div class="page-shell treelife-info-page">
    <header class="treelife-hero">
      <RouterLink class="treelife-badge" to="/showcase" aria-label="返回作品页面">
        <span aria-hidden="true">✦</span>
        TreeLife
      </RouterLink>
      <p class="eyebrow">Privacy policy</p>
      <h1>隐私政策</h1>
      <p class="hero-copy">你的计划、专注与成长记录属于你。TreeLife 以本地存储为基础，不出售数据，也不进行广告追踪。</p>
      <p class="updated-at">生效日期：2026 年 10 月 18 日</p>
    </header>

    <div class="treelife-info-layout">
      <aside class="summary-card surface" aria-label="隐私摘要">
        <span class="summary-icon" aria-hidden="true">◌</span>
        <h2>隐私摘要</h2>
        <ul>
          <li>无需注册账号</li>
          <li>不收集个人数据</li>
          <li>不含广告或跨应用追踪</li>
          <li>成长记录保存在设备本地</li>
        </ul>
      </aside>

      <article class="policy-content surface">
        <section>
          <span class="section-number">01</span>
          <div>
            <h2>我们收集哪些信息</h2>
            <p>TreeLife 当前不要求创建账号，也不会把你的个人信息、任务内容或使用记录上传至开发者服务器。App 不包含广告、行为分析或跨应用追踪功能。</p>
          </div>
        </section>

        <section>
          <span class="section-number">02</span>
          <div>
            <h2>设备上的本地数据</h2>
            <p>你创建的长期树、短期树、每日任务、任务森林、完成状态、番茄钟专注时长、果实记录和个性化设置均保存在你的设备本地，用于提供 App 的核心功能。</p>
            <p>删除 App 通常会一并移除这些本地数据；如果你的设备启用了系统备份，备份副本的保留与恢复由你的 Apple 设备及 Apple 账户设置管理。</p>
          </div>
        </section>

        <section>
          <span class="section-number">03</span>
          <div>
            <h2>通知权限</h2>
            <p>TreeLife 仅在你主动允许后使用系统通知，提醒任务或专注计时。通知由设备本地安排，我们不会收集通知内容。你可以随时在 iOS“设置”中关闭通知权限。</p>
          </div>
        </section>

        <section>
          <span class="section-number">04</span>
          <div>
            <h2>第三方共享与服务</h2>
            <p>TreeLife 当前不向第三方出售、出租或共享你的数据，也未集成用于广告投放、用户画像或追踪的第三方服务。</p>
          </div>
        </section>

        <section>
          <span class="section-number">05</span>
          <div>
            <h2>未来功能与政策更新</h2>
            <p>如果未来版本加入账号、云同步或社区等需要处理数据的功能，我们会在功能上线前更新本政策，并按照适用要求向你说明相关的数据用途和选择。</p>
          </div>
        </section>

        <section>
          <span class="section-number">06</span>
          <div>
            <h2>联系我们</h2>
            <p>如果你对本隐私政策或 TreeLife 的数据处理方式有任何疑问，请发送邮件至：</p>
            <a class="contact-link" href="mailto:magnolia71102@gmail.com?subject=TreeLife%20隐私问题">
              magnolia71102@gmail.com
              <span aria-hidden="true">↗</span>
            </a>
          </div>
        </section>
      </article>
    </div>

    <nav class="related-page surface" aria-label="相关页面">
      <div>
        <p class="eyebrow">Need help?</p>
        <strong>使用 TreeLife 时遇到问题？</strong>
      </div>
      <RouterLink to="/treelife/support">前往技术支持 <span aria-hidden="true">→</span></RouterLink>
    </nav>
  </div>
</template>

<style scoped src="../styles/treelife-info.css"></style>
