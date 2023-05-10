//
//  HomeView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 5/5/2023.
//

import SwiftUI


// iosacademy tutorial
struct Store: Hashable, Codable {
    let sname: String
    //let image: String
}


// iosacademy tutorial
class ViewModel: ObservableObject {
    @Published var stores: [Store] = []
    
    //http://localhost:5000/api/items
    func fetch() {
        //guard let url = URL(string: "https://iosacademy.io/api/v1/courses/index.php") else {
            //return
        guard let url = URL(string: "http://localhost:5005/store") else {
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { [weak self] data, _,
            error in
            guard let data = data, error == nil else {
                return
            }
            
            // convert to JSON
            do {
                let stores = try JSONDecoder().decode([Store].self, from: data)
                DispatchQueue.main.async {
                    self?.stores = stores
                }
            }
            catch {
                print(error)
            }
        }
        task.resume()
    }
}

struct HomeView: View {
    @StateObject var viewModel = ViewModel()
    @State private var searchText = ""
    //private var products : [Product] = Product.allProducts
    //let allProducts = ["Apple", "Banana", "Cucumber"]
    
    var body: some View {
        NavigationView {
            VStack {
                
                List {
                    ForEach(viewModel.stores, id: \.self) { store in
                        HStack {
                            //Image("")
                                //.frame(width: 120, height: 60)
                                //.background(Color.gray)
                            
                            
                            Text(store.sname)
                                .bold()
                        }
                        .padding(3)
                    }
                }
                
                /*
                List {
                    // ideally the id should be unique
                    ForEach(products, id: \.shopName) { product in
                        Text("\(product.shopName)")
                        Text("\(product.address.streetAddress)")
                    }
                }*/
                
                /*
                List {
                    // ideally the id should be unique
                    ForEach(filteredItems, id: \.self) { product in
                        Text(product)
                    }
                }*/
                
                //LazyVGrid
            }
            .searchable(text: $searchText, prompt: "Search")
            .navigationBarTitle("Home")
            // from the iosacademy tutorial
            
            .onAppear {
                viewModel.fetch()
            }
        }
    }
    
    /*
    var filteredItems: [String] {
        if searchText.isEmpty {
            return allProducts
        } else {
            return allProducts.filter { $0.localizedCaseInsensitiveContains(searchText)}
        }
    }*/

}

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView()
    }
}
