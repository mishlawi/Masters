package eu.europa.esig.dss.web.controller;

import eu.europa.esig.dss.web.model.User;
import eu.europa.esig.dss.web.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.sql.SQLException;

@Controller
public class SignUpController {

    @Autowired
    private LoginService loginService;

    @GetMapping(value = "/signup")
    public String showRegistrationForm(Model model) {
        User user = new User();
        user.setTelemovel("+351 ");
        model.addAttribute("user", user);

        return "signup";
    }

    @PostMapping(value = "/signup_process")
    public String processRegister(@ModelAttribute("user") @Valid User user) throws SQLException {
        boolean f = this.loginService.validateUser(user.getUsername());
        if (f) {
            BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
            String encodedPassword = passwordEncoder.encode(user.getPassword());
            user.setPassword(encodedPassword);
            this.loginService.addUser(user.getUsername(), user.getPassword());
            return "login";
        } else{

            return "signup";
        }
    }
}
