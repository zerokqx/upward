import { useState } from 'react'
import './counter.css'

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button
      type="button"
      className="counter"
      onClick={() => setCount((prev) => prev + 1)}
    >
      Count is {count}
    </button>
  )
}
