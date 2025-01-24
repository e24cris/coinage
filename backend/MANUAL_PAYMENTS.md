# Coinage Manual Payment System

## Overview
The Coinage platform implements a manual payment system where users can request wallet funding, and admins manually approve these requests.

## Payment Request Workflow

### User Flow
1. User logs into their account
2. Navigate to the wallet funding section
3. Select cryptocurrency for deposit
4. Enter deposit amount
5. Provide wallet address for transfer
6. (Optional) Upload proof of payment
7. Submit payment request

### Admin Approval Process
1. Admin logs into the system
2. Views pending payment requests
3. Verifies payment details
4. Can:
   - Approve the request (adds funds to user's account)
   - Reject the request (with optional notes)

## API Endpoints

### User Endpoints
- `POST /payments/request`
  - Create a new payment request
  - Required fields: 
    - `amount`: Deposit amount
    - `cryptocurrency`: BTC, ETH, etc.
    - `wallet_address`: User's wallet address
  - Optional: `proof_of_payment` file upload

- `GET /payments/requests`
  - Retrieve user's own payment requests

### Admin Endpoints
- `GET /payments/admin/requests`
  - Retrieve all pending payment requests

- `POST /payments/admin/process/<request_id>`
  - Process a payment request
  - Actions: 'approve' or 'reject'
  - Optional: provide transaction hash, admin notes

## Security Considerations
- Only admin users can approve/reject requests
- Payment proofs are stored securely
- Transactions are logged for audit purposes

## Supported Cryptocurrencies
- Bitcoin (BTC)
- Ethereum (ETH)
- Other cryptocurrencies can be added as needed

## Best Practices
- Always verify wallet addresses
- Keep transaction records
- Communicate clearly with users about request status

## Troubleshooting
- Ensure correct wallet addresses
- Check cryptocurrency network status
- Verify transaction confirmations

## Future Improvements
- Automated transaction verification
- Real-time blockchain transaction tracking
- Enhanced admin dashboard
