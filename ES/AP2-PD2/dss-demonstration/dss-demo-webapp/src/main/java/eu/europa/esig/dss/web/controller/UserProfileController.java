package eu.europa.esig.dss.web.controller;

import eu.europa.esig.dss.web.model.User;
import eu.europa.esig.dss.web.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

import javax.validation.Valid;
import java.sql.SQLException;

@Controller
public class UserProfileController {

    private DriverManagerDataSource dataSource;


    @Autowired
    private LoginService loginService;

    private String getLoggedUser(){
        Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        String username;
        if (principal instanceof UserDetails) {
            username = ((UserDetails)principal).getUsername();
        } else {
            username = principal.toString();
        }
        return username;
    }


    @GetMapping("/user-profile")
    public String show(Model model) throws SQLException {

        User user = new User();
        String username = this.getLoggedUser();
        user.setUsername(username);
        model.addAttribute("user", user);

        return "user-profile";
    }

    @PostMapping("/update-phone-number")
    public String update(@ModelAttribute("user") @Valid User user) throws SQLException {
        String telemovel = user.getTelemovel();
        String username = this.getLoggedUser();
        this.loginService.setTelemovel(username,telemovel);

        return "user-profile";
    }
}
