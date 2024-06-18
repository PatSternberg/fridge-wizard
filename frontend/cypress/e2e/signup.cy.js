describe('User signup', () => {
  it('Signs up a new user', () => {
    // Navigate to the Fridge Wizard landing page
    cy.visit('localhost:3000/')

    // Click the signup link
    cy.contains('Sign up').click()

    // Verify that the new page contains the signup form
    cy.get('form')

    // Fill out the email, username and password fields
    cy.get('form:has(label:contains("Email"))')
    .find('div:has(label:contains("Email"))')
    .find('input')
    .type('testEmail@email.com')

    cy.get('form:has(label:contains("Username"))')
    .find('div:has(label:contains("Username"))')
    .find('input')
    .type('testUsername')

    cy.get('form:has(label:contains("Password"))')
    .find('div:has(label:contains("Password"))')
    .find('input')
    .type('testPassword!')

    // Verify that the form is filled out as expected
    cy.get('form:has(label:contains("Email"))')
    .find('div:has(label:contains("Email"))')
    .find('input')
    .should('have.value', 'testEmail@email.com')

    cy.get('form:has(label:contains("Username"))')
    .find('div:has(label:contains("Username"))')
    .find('input')
    .should('have.value', 'testUsername')

    cy.get('form:has(label:contains("Password"))')
    .find('div:has(label:contains("Password"))')
    .find('input')
    .should('have.value', 'testPassword!')

    // Signup the test user
    cy.contains('Sign up').click()

    // Verify that the signup was successful and navigated
    // to the fridge page
    cy.url().should('include', '/fridge/')
    cy.contains('My fridge')
    
  })
})