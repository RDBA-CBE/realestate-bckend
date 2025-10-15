# Updated User Signup Flow - Admin Approval Required

## Overview
All new users must now get admin approval before they can login to the platform.

## User Registration Flow

### 1. User Registration
**Endpoint**: `POST /api/auth/register/`

**Request**:
```json
{
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "user_type": "buyer",
    "password": "securepassword123",
    "terms_accepted": true
}
```

**Response**:
```json
{
    "success": "User created successfully",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "user_type": "buyer",
        "account_status": "pending_review",
        "requires_admin_approval": true
    },
    "message": "Registration successful! Your account has been submitted for admin review. You will receive an email notification once your account is approved and you can login.",
    "next_steps": [
        "Wait for admin review and approval",
        "Check your email for approval notification",
        "Complete your profile after approval (if required)"
    ]
}
```

**What happens**:
- User account is created with `is_active = False`
- Account status set to `pending_review`
- User cannot login until approved
- Admins receive notification email

### 2. Check Registration Status (Public)
**Endpoint**: `POST /api/auth/register/check_status/`

**Request**:
```json
{
    "email": "user@example.com"
}
```

**Response**:
```json
{
    "email": "user@example.com",
    "account_status": "pending_review",
    "status_message": "Account under admin review",
    "can_login": false,
    "user_type": "buyer",
    "created_at": "2025-10-15T10:30:00Z",
    "approved_at": null,
    "rejection_reason": null
}
```

## Admin Approval Process

### 3. View Pending Approvals (Admin Only)
**Endpoint**: `GET /api/auth/register/pending_approvals/`

**Response**:
```json
[
    {
        "id": 1,
        "email": "user@example.com",
        "name": "John Doe",
        "user_type": "buyer",
        "account_status": "pending_review",
        "created_at": "2025-10-15T10:30:00Z",
        "profile_completed": false,
        "documents_uploaded": false,
        "profile_completion_percentage": 0
    }
]
```

### 4. Approve User Account (Admin Only)
**Endpoint**: `POST /api/auth/register/approve_account/`

**Request**:
```json
{
    "user_id": 1,
    "action": "approved",
    "notes": "Account approved - all requirements met"
}
```

**Response**:
```json
{
    "success": "Account approved successfully",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "user_type": "buyer",
        "account_status": "approved",
        "approved_at": "2025-10-15T11:00:00Z"
    }
}
```

**What happens**:
- User's `is_active` is set to `True`
- Account status changed to `approved`
- User can now login
- User receives approval email notification

### 5. Reject User Account (Admin Only)
**Endpoint**: `POST /api/auth/register/approve_account/`

**Request**:
```json
{
    "user_id": 1,
    "action": "rejected",
    "rejection_reason": "Incomplete documentation provided"
}
```

**Response**:
```json
{
    "success": "Account rejected successfully",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "user_type": "buyer",
        "account_status": "rejected",
        "approved_at": null
    }
}
```

## User Login & Dashboard Access

### 6. Login Attempt
- Users with `account_status = "pending_review"` or `"rejected"` cannot login
- Only users with `account_status = "approved"` and `is_active = True` can login

### 7. Check Account Status (Authenticated)
**Endpoint**: `GET /api/auth/dashboard/account_status/`

**Response for pending user**:
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "name": "John Doe",
        "user_type": "buyer",
        "account_status": "pending_review",
        "is_active": false,
        "can_access_platform": false
    },
    "status_info": {
        "pending_review": true,
        "approved": false,
        "rejected": false,
        "rejection_reason": null
    }
}
```

### 8. Dashboard Access (Authenticated & Approved Only)
**Endpoint**: `GET /api/auth/dashboard/dashboard_data/`

**Response for non-approved users**:
```json
{
    "message": "Your account is under review",
    "account_status": "pending_review",
    "user_type": "buyer",
    "next_steps": [
        "Wait for admin approval",
        "Check your email for updates",
        "Contact support if you have questions"
    ]
}
```

## Email Notifications

### Admin Notification (New Registration)
- Sent to all admin users when new user registers
- Contains user details and link to admin panel

### User Notification (Approval/Rejection)
- Sent when admin approves or rejects account
- Contains next steps and relevant information

## Security Features

1. **No Auto-Activation**: All users start with `is_active = False`
2. **Admin Only Approval**: Only admin users can approve/reject accounts
3. **Status Tracking**: Complete audit trail of account status changes
4. **Email Notifications**: Automated notifications for status changes
5. **Public Status Check**: Users can check their application status without logging in
6. **Dashboard Protection**: Dashboard access restricted to approved users only

## Available Endpoints Summary

| Endpoint | Method | Access | Purpose |
|----------|--------|--------|---------|
| `/api/auth/register/` | POST | Public | User registration |
| `/api/auth/register/check_status/` | POST | Public | Check registration status |
| `/api/auth/register/pending_approvals/` | GET | Admin | View pending approvals |
| `/api/auth/register/approve_account/` | POST | Admin | Approve/reject accounts |
| `/api/auth/dashboard/account_status/` | GET | Authenticated | Check own account status |
| `/api/auth/dashboard/dashboard_data/` | GET | Approved Users | Access dashboard |