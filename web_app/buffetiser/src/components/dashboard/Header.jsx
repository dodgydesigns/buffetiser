import PropTypes from 'prop-types'
import React from 'react'

function Header({ text }) {
  /* This is the header for the whole page. It might just contain navigation stuff. */
  return (
    <header>
      <div>
        <h2>{text}</h2>
      </div>
    </header>
  )
}

export default Header

Header.defaultProps = {
  text: "Buffetiser"
}

Header.prototypes = {
  text: PropTypes.string.isRequired
}