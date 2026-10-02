import { Counter } from '@/features/counter'
import { heroImg, reactLogo, viteLogo } from '@/shared/assets'
import './hero.css'

export function Hero() {
  return (
    <section id="center">
      <div className="hero">
        <img src={heroImg} className="base" width="170" height="179" alt="" />
        <img src={reactLogo} className="framework" alt="React logo" />
        <img src={viteLogo} className="vite" alt="Vite logo" />
      </div>
      <div>
        <h1>Get started</h1>
        <p>
          Edit <code>src/pages/home/ui/home-page.tsx</code> and save to test <code>HMR</code>
        </p>
      </div>
      <Counter />
    </section>
  )
}
