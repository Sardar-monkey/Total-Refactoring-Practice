import java.util.Objects;

public final class Address {
    private final String address;
    private final String city;
    private final String zipCode;
    private final String country;

    public Address(String address, String city, String zipCode, String country) {
        this.address = address;
        this.city = city;
        this.zipCode = zipCode;
        this.country = country;
    }

    public String getFullAddress() {
        return address + ", " + city + ", " + zipCode + ", " + country;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Address)) return false;
        Address that = (Address) o;
        return Objects.equals(address, that.address) &&
               Objects.equals(city, that.city) &&
               Objects.equals(zipCode, that.zipCode) &&
               Objects.equals(country, that.country);
    }

    @Override
    public int hashCode() {
        return Objects.hash(address, city, zipCode, country);
    }
}