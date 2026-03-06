#!/usr/bin/env python3
"""
Session 08: Secure Vault
Secure credential storage and sharing between agents.
"""

import json
import base64
import hashlib
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets


@dataclass
class Credential:
    """A stored credential."""
    key: str  # Name/identifier
    value: str  # Encrypted value
    owner: str  # Agent that created it
    created_at: str
    shared_with: List[str]  # Agents that can access it
    access_count: int = 0
    last_accessed: Optional[str] = None


class SecureVault:
    """
    Secure credential vault with encryption.
    
    Features:
    - Encryption at rest
    - Access control (owner-based)
    - Audit trail
    - Secure sharing between agents
    """
    
    def __init__(self, vault_path: str = "vault/credentials.json", master_key: str = None):
        self.vault_path = Path(vault_path)
        self.vault_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize encryption
        self.master_key = master_key or self._generate_key()
        self.fernet = Fernet(self.master_key)
        
        # Load existing credentials
        self.credentials: Dict[str, Credential] = {}
        self._load()
    
    def _generate_key(self) -> bytes:
        """Generate encryption key from password or random."""
        # In production, use a proper password-based KDF
        # Here we use a simple approach for demonstration
        password = secrets.token_urlsafe(32).encode()
        salt = secrets.token_bytes(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def _load(self):
        """Load credentials from disk."""
        if self.vault_path.exists():
            try:
                with open(self.vault_path, 'r') as f:
                    data = json.load(f)
                    for key, cred_dict in data.items():
                        self.credentials[key] = Credential(**cred_dict)
            except Exception as e:
                print(f"[VAULT] Warning: Could not load vault: {e}")
    
    def _save(self):
        """Save credentials to disk."""
        data = {key: asdict(cred) for key, cred in self.credentials.items()}
        with open(self.vault_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def store(self, key: str, value: str, owner: str = "agent") -> bool:
        """
        Store a credential securely.
        
        The value is encrypted before storage.
        """
        try:
            # Encrypt the value
            encrypted = self.fernet.encrypt(value.encode()).decode()
            
            # Store metadata
            credential = Credential(
                key=key,
                value=encrypted,
                owner=owner,
                created_at=datetime.now().isoformat(),
                shared_with=[owner]  # Owner has access by default
            )
            
            self.credentials[key] = credential
            self._save()
            
            print(f"[VAULT] ✓ Stored credential '{key}' (owner: {owner})")
            return True
        
        except Exception as e:
            print(f"[VAULT] ✗ Failed to store '{key}': {e}")
            return False
    
    def retrieve(self, key: str, requester: str = "agent") -> Optional[str]:
        """
        Retrieve and decrypt a credential.
        
        Only the owner or explicitly shared agents can retrieve.
        """
        if key not in self.credentials:
            print(f"[VAULT] ✗ Credential '{key}' not found")
            return None
        
        credential = self.credentials[key]
        
        # Check access
        if requester not in credential.shared_with:
            print(f"[VAULT] ✗ Access denied for '{key}' (requester: {requester})")
            return None
        
        try:
            # Decrypt
            decrypted = self.fernet.decrypt(credential.value.encode()).decode()
            
            # Update audit trail
            credential.access_count += 1
            credential.last_accessed = datetime.now().isoformat()
            self._save()
            
            print(f"[VAULT] ✓ Retrieved '{key}' (access #{credential.access_count})")
            return decrypted
        
        except Exception as e:
            print(f"[VAULT] ✗ Failed to decrypt '{key}': {e}")
            return None
    
    def share(self, key: str, owner: str, recipient: str) -> bool:
        """
        Share a credential with another agent.
        
        Only the owner can share.
        """
        if key not in self.credentials:
            print(f"[VAULT] ✗ Credential '{key}' not found")
            return False
        
        credential = self.credentials[key]
        
        if credential.owner != owner:
            print(f"[VAULT] ✗ Only owner can share '{key}'")
            return False
        
        if recipient not in credential.shared_with:
            credential.shared_with.append(recipient)
            self._save()
            print(f"[VAULT] ✓ Shared '{key}' with {recipient}")
        else:
            print(f"[VAULT] ℹ '{key}' already shared with {recipient}")
        
        return True
    
    def revoke(self, key: str, owner: str, recipient: str) -> bool:
        """Revoke access from an agent."""
        if key not in self.credentials:
            return False
        
        credential = self.credentials[key]
        
        if credential.owner != owner:
            print(f"[VAULT] ✗ Only owner can revoke '{key}'")
            return False
        
        if recipient in credential.shared_with and recipient != owner:
            credential.shared_with.remove(recipient)
            self._save()
            print(f"[VAULT] ✓ Revoked '{key}' from {recipient}")
            return True
        
        return False
    
    def delete(self, key: str, owner: str) -> bool:
        """Delete a credential (owner only)."""
        if key not in self.credentials:
            return False
        
        if self.credentials[key].owner != owner:
            print(f"[VAULT] ✗ Only owner can delete '{key}'")
            return False
        
        del self.credentials[key]
        self._save()
        print(f"[VAULT] ✓ Deleted '{key}'")
        return True
    
    def list_credentials(self, requester: str = None) -> List[str]:
        """List credentials accessible to requester."""
        if requester:
            return [
                key for key, cred in self.credentials.items()
                if requester in cred.shared_with
            ]
        return list(self.credentials.keys())
    
    def audit_log(self, key: str = None) -> str:
        """Get audit information."""
        lines = ["=== VAULT AUDIT LOG ==="]
        
        creds = [self.credentials[key]] if key else self.credentials.values()
        
        for cred in creds:
            lines.append(f"\nCredential: {cred.key}")
            lines.append(f"  Owner: {cred.owner}")
            lines.append(f"  Shared with: {', '.join(cred.shared_with)}")
            lines.append(f"  Created: {cred.created_at}")
            lines.append(f"  Access count: {cred.access_count}")
            lines.append(f"  Last accessed: {cred.last_accessed or 'Never'}")
        
        return "\n".join(lines)


def main():
    print("⚔️ Ares Session 08: Secure Vault")
    print("Secure credential storage and sharing.\n")
    
    # Create vault
    vault = SecureVault()
    
    print("Commands:")
    print("  store <key> <value> <owner>  - Store credential")
    print("  get <key> <requester>        - Retrieve credential")
    print("  share <key> <owner> <to>     - Share credential")
    print("  revoke <key> <owner> <from>  - Revoke access")
    print("  list [requester]             - List accessible credentials")
    print("  audit [key]                  - View audit log")
    print("  exit                         - Quit")
    print()
    
    # Demo
    print("Demo: Storing API keys...")
    vault.store("OPENAI_API_KEY", "sk-abc123", owner="agent1")
    vault.store("DATABASE_URL", "postgresql://...", owner="agent1")
    vault.store("STRIPE_KEY", "sk_live_...", owner="agent2")
    print()
    
    print("Demo: Retrieving...")
    key = vault.retrieve("OPENAI_API_KEY", requester="agent1")
    print(f"Retrieved: {key}\n")
    
    print("Demo: Sharing...")
    vault.share("OPENAI_API_KEY", owner="agent1", recipient="agent2")
    print()
    
    print("Demo: Access control...")
    vault.retrieve("OPENAI_API_KEY", requester="agent3")  # Should fail
    print()
    
    print(vault.audit_log())


if __name__ == "__main__":
    # Note: cryptography library required
    # pip install cryptography
    try:
        from cryptography.fernet import Fernet
        main()
    except ImportError:
        print("This session requires the 'cryptography' library.")
        print("Install it: pip install cryptography")
        print("\nFor now, here's the concept:")
        print("- Credentials are encrypted before storage")
        print("- Only owner and shared agents can decrypt")
        print("- Access is logged for audit")
        print("- Owner can revoke access anytime")
