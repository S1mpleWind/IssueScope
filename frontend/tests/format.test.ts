import { describe, expect, it } from 'vitest'

import { formatProjectCategory } from '../src/utils/format'

describe('formatProjectCategory', () => {
  it('shows the Chinese label for a known project category', () => {
    expect(formatProjectCategory('source_code')).toBe('Source code')
  })

  it('humanizes an unknown project category', () => {
    expect(formatProjectCategory('integration_test')).toBe('integration test')
  })
})
