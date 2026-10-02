import { Hero } from '@/widgets/hero'
import { NextSteps } from '@/widgets/next-steps'
import { Spacer, Ticks } from '@/shared/ui'

export function HomePage() {
  return (
    <>
      <Hero />
      <Ticks />
      <NextSteps />
      <Ticks />
      <Spacer />
    </>
  )
}
