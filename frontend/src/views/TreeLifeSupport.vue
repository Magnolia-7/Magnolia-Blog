<template>
  <div class="page-shell treelife-info-page">
    <header class="treelife-hero support-hero">
      <RouterLink class="treelife-badge" to="/showcase" aria-label="返回作品页面">
        <span aria-hidden="true">✦</span>
        TreeLife
      </RouterLink>
      <p class="eyebrow">Support</p>
      <h1>技术支持</h1>
      <p class="hero-copy">无论是使用疑问、功能建议还是异常反馈，都可以从这里联系 TreeLife。</p>
      <a class="primary-contact" href="mailto:magnolia71102@gmail.com?subject=TreeLife%20技术支持">
        <span>
          <small>联系邮箱</small>
          <strong>magnolia71102@gmail.com</strong>
        </span>
        <i aria-hidden="true">↗</i>
      </a>
    </header>

    <section class="support-intro surface">
      <div>
        <p class="eyebrow">Before contacting</p>
        <h2>为了更快定位问题</h2>
      </div>
      <p>请在邮件中附上 TreeLife 版本、iOS 版本、问题发生前的操作步骤；如果方便，也可以附上不会暴露私人任务内容的截图或录屏。</p>
    </section>

    <section class="faq-section">
      <div class="section-heading">
        <p class="eyebrow">Frequently asked</p>
        <h2>常见问题</h2>
      </div>

      <div class="faq-grid">
        <article class="surface">
          <span>01</span>
          <h3>需要注册账号吗？</h3>
          <p>不需要。TreeLife 当前没有账号系统，打开 App 后即可开始创建和管理自己的成长计划。</p>
        </article>
        <article class="surface">
          <span>02</span>
          <h3>我的任务记录存在哪里？</h3>
          <p>长期树、短期树、每日任务、专注时长和果实记录均保存在设备本地，目前不会同步到开发者服务器。</p>
        </article>
        <article class="surface">
          <span>03</span>
          <h3>为什么收不到提醒？</h3>
          <p>请前往 iPhone“设置”→“通知”→“TreeLife”，确认允许通知。专注模式或系统通知摘要也可能影响提醒出现的时间。</p>
        </article>
        <article class="surface">
          <span>04</span>
          <h3>删除 App 后数据还能恢复吗？</h3>
          <p>TreeLife 的数据保存在本机，删除 App 可能同时删除本地记录。是否能通过设备备份恢复，取决于你的 Apple 设备和账户备份设置。</p>
        </article>
        <article class="surface">
          <span>05</span>
          <h3>如何反馈功能建议？</h3>
          <p>欢迎直接发送邮件，说明希望解决的场景和理想效果。TestFlight 测试用户也可以通过 TestFlight 提交反馈。</p>
        </article>
        <article class="surface">
          <span>06</span>
          <h3>出现异常应该提供什么？</h3>
          <p>请描述复现步骤、实际结果和预期结果，并附上设备型号、iOS 版本与 App 版本，以便更准确地排查。</p>
        </article>
      </div>
    </section>

    <section class="support-callout">
      <span class="callout-mark" aria-hidden="true">M</span>
      <div>
        <p class="eyebrow">Write to us</p>
        <h2>没有找到答案？</h2>
        <p>把你遇到的问题告诉我们，我们会认真阅读并尽快处理。</p>
      </div>
      <a href="mailto:magnolia71102@gmail.com?subject=TreeLife%20问题反馈">发送邮件 <span aria-hidden="true">→</span></a>
    </section>

    <nav class="related-page surface" aria-label="相关页面">
      <div>
        <p class="eyebrow">Your privacy</p>
        <strong>了解 TreeLife 如何保护你的数据</strong>
      </div>
      <RouterLink to="/treelife/privacy">查看隐私政策 <span aria-hidden="true">→</span></RouterLink>
    </nav>
  </div>
</template>

<style scoped src="../styles/treelife-info.css"></style>
