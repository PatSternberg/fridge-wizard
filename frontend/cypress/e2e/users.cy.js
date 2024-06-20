describe('User signup and login', () => {
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

  it('Logs in an existing user', () => {
    // Navigate to the Fridge Wizard landing page
    cy.visit('localhost:3000/')

    // Click the login link
    cy.contains('Log in').click()

    // Verify that the new page contains the login form
    cy.get('form')

    // Fill out the email and password fields
    cy.get('form:has(label:contains("Email"))')
    .find('div:has(label:contains("Email"))')
    .find('input')
    .type('testEmail@email.com')

    cy.get('form:has(label:contains("Password"))')
    .find('div:has(label:contains("Password"))')
    .find('input')
    .type('testPassword!')

    // Verify that the form is filled out as expected
    cy.get('form:has(label:contains("Email"))')
    .find('div:has(label:contains("Email"))')
    .find('input')
    .should('have.value', 'testEmail@email.com')

    cy.get('form:has(label:contains("Password"))')
    .find('div:has(label:contains("Password"))')
    .find('input')
    .should('have.value', 'testPassword!')

    // Login the test user
    cy.get('form')
    .contains('Log in').click()

    // Verify that the signup was successful and navigated
    // to the fridge page
    cy.url().should('include', '/fridge/')
    cy.contains('My fridge')
  })
})

describe('Add and remove items from fridge', () => {
  it("Adds an item to a user's fridge", () => {
    // Navigate to the Fridge Wizard landing page and log in
    cy.visit('localhost:3000/')
    cy.contains('Log in').click()
    
    cy.get('form').within(() => {
      cy.get('label:contains("Email")').parent().find('input').type('testEmail@email.com')
      cy.get('label:contains("Password")').parent().find('input').type('testPassword!')
    })
    
    cy.get('form').contains('Log in').click()
  
    // Verify that the login was successful and navigated to the fridge page
    cy.url().should('include', '/fridge/')
    cy.contains('My fridge')
  
    // Adds an item to the fridge
    cy.contains('button', 'Add Items').click()
  
    // Verify that the form is displayed
    cy.get('select').should('exist').and('be.visible')
  
    // Select the "Choose Category..." option
    cy.get('select').select('Choose Category...')
  
    // Selecting a specific category, entering item name, setting expiry date
    cy.get('select').select('🍉 Fruit')
    cy.get('input[placeholder="Item Name"]').type('Pear')
    cy.get('input[type="date"]').type('2025-01-01')
  
    // Submit the form
    cy.contains('button', 'Submit All Items').click()
  
    // Verify the item was added to the fridge
    cy.contains('Pear').should('exist')
  })

    it("Deletes an item from a user's fridge", () => {
    // Navigate to the Fridge Wizard landing page and log in
    cy.visit('localhost:3000/')
    cy.contains('Log in').click()
    cy.get('form:has(label:contains("Email"))')
    .find('div:has(label:contains("Email"))')
    .find('input')
    .type('testEmail@email.com')
    cy.get('form:has(label:contains("Password"))')
    .find('div:has(label:contains("Password"))')
    .find('input')
    .type('testPassword!')
    cy.get('form')
    .contains('Log in').click()

    // Verify that the login was successful and navigated
    // to the fridge page
    cy.url().should('include', '/fridge/')
    cy.contains('My fridge')
    
    // Removes an item from the fridge
    // Find the list item containing 'Hot sauce'
    cy.get('li.item').contains('Pear').should('exist').parent().find('button').should('exist').and('be.visible').click();

    // Verify the item was removed from the fridge
    cy.contains('Pear').should('not.exist')
  })
})