package eu.europa.esig.dss.web.service;

import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.stereotype.Component;

import java.sql.ResultSet;
import java.sql.SQLException;

@Component
public class LoginService {

    private final DriverManagerDataSource dataSource;

    public LoginService(){
        DriverManagerDataSource dataSourceBuilder = new DriverManagerDataSource();
        dataSourceBuilder.setDriverClassName("com.mysql.jdbc.Driver");
        dataSourceBuilder.setUrl("jdbc:mysql://localhost:3306/pd2?serverTimezone=UTC&useSSL=false");
        dataSourceBuilder.setUsername("root");
        dataSourceBuilder.setPassword("root");

        this.dataSource = dataSourceBuilder;
    }

    public String getTelemovel(String username) throws SQLException {
        String query = "Select telemovel from users where username='"  + username + "';";
        ResultSet res = this.dataSource.getConnection().prepareStatement(query).executeQuery();
        res.next();
        return res.getString("telemovel");
    }

    public void setTelemovel(String username, String telemovel) throws SQLException {
        this.dataSource.getConnection()
                .prepareStatement("UPDATE users SET telemovel = '" + telemovel + "' WHERE (username = '" + username + "');").execute();
    }

    public void addUser(String username, String password, String telemovel) throws SQLException {
        this.dataSource.getConnection().prepareStatement("insert users(username, password, telemovel) values ('"
                + username + "', '" + password + "','" + telemovel + "');").execute();
    }

    public void addUser(String username, String password) throws SQLException {
        this.dataSource.getConnection().prepareStatement("insert users(username, password) values ('"
                + username + "', '" + password + "');").execute();
    }

    public boolean validateUser(String username) throws SQLException {
        String query = "Select * from users where username='"  + username + "';";
        ResultSet res = this.dataSource.getConnection().prepareStatement(query).executeQuery();
        return !res.isBeforeFirst();
    }
}
