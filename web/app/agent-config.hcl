pid_file = "./pidfile"
exit_after_auth = true


vault {
   address = "http://vault:8200"
   tls_skip_verify = true
}

auto_auth {
   method {
      type = "token_file"
      config = {
         token_file_path = "./.vault-token"
      }
   }
}
