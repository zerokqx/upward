import { reactLogo, viteLogo } from '@/shared/assets'
import { Icon } from '@/shared/ui'
import './next-steps.css'

export function NextSteps() {
  return (
    <section id="next-steps">
      <div id="docs">
        <Icon name="documentation-icon" className="icon" />
        <h2>Documentation</h2>
        <p>Your questions, answered</p>
        <ul>
          <li>
            <a href="https://vite.dev/" target="_blank" rel="noreferrer">
              <img className="logo" src={viteLogo} alt="" />
              Explore Vite
            </a>
          </li>
          <li>
            <a href="https://react.dev/" target="_blank" rel="noreferrer">
              <img className="button-icon" src={reactLogo} alt="" />
              Learn more
            </a>
          </li>
        </ul>
      </div>
      <div id="social">
        <Icon name="social-icon" className="icon" />
        <h2>Connect with us</h2>
        <p>Join the Vite community</p>
        <ul>
          <li>
            <a href="https://github.com/vitejs/vite" target="_blank" rel="noreferrer">
              <Icon name="github-icon" className="button-icon" />
              GitHub
            </a>
          </li>
          <li>
            <a href="https://chat.vite.dev/" target="_blank" rel="noreferrer">
              <Icon name="discord-icon" className="button-icon" />
              Discord
            </a>
          </li>
          <li>
            <a href="https://x.com/vite_js" target="_blank" rel="noreferrer">
              <Icon name="x-icon" className="button-icon" />
              X.com
            </a>
          </li>
          <li>
            <a href="https://bsky.app/profile/vite.dev" target="_blank" rel="noreferrer">
              <Icon name="bluesky-icon" className="button-icon" />
              Bluesky
            </a>
          </li>
        </ul>
      </div>
    </section>
  )
}
