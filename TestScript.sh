#!/bin/bash

n=100

# Item 1: image1 to image3 (comparison within same item images)
echo "=== Matching within Item-1 (image1–image3) ==="
for i in {1..3}; do
  for j in {1..3}; do
    if [ "$i" -ne "$j" ]; then
      echo "Comparing ./Item1/image$i.jpg vs /Item1/image$j.jpg"
       ./ORB_Python.sh "$n" ./Images/Item1/"image$i.jpg" ./Images/Item1/"image$j.jpg"
    fi
  done
done

# Item 2: image1 to image3 (comparison within same item images)
echo -e "\n=== Matching within Item-2 (image1–image3) ==="
for i in {1..3}; do
  for j in {1..3}; do
    if [ "$i" -ne "$j" ]; then
      echo "Comparing ./Item2/image$i.jpg vs /Item2/image$j.jpg"
      ./ORB_Python.sh "$n" ./Images/Item2/"image$i.jpg" ./Images/Item2/"image$j.jpg"
    fi
  done
done


# Separator
echo -e "\n-------------------------------------------------"
echo "=== Cross-item comparisons (Item-1 images vs Item-2 images) ==="

# Cross-item-matching: Item-1 images vs Item-2 images
for i in {1..3}; do
  for j in {1..3}; do
    echo "Comparing ./Item1/image$i.jpg vs /Item2/image$j.jpg"
    ./ORB_Python.sh "$n" ./Images/Item1/"image$i.jpg" ./Images/Item2/"image$j.jpg"
  done
done


echo -e "\n=== Cross-item comparisons (Item-2 images vs Item-1 images) ==="

# Cross-item-matching: Item-2 images vs Item-1 images
for i in {1..3}; do
  for j in {1..3}; do
    echo "Comparing ./Item2/image$i.jpg vs /Item1/image$j.jpg"
    ./ORB_Python.sh "$n" ./Images/Item2/"image$i.jpg" ./Images/Item1/"image$j.jpg"
  done
done
